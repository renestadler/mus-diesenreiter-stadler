package at.fhooe.recyclingserver.jpa;

import at.fhooe.recyclingserver.model.Product;
import at.fhooe.recyclingserver.model.RecyclingInfo;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface RecyclingInfoRepository extends JpaRepository<RecyclingInfo, Long> {
    Optional<RecyclingInfo> findFirstByMaterial(String material);
}

