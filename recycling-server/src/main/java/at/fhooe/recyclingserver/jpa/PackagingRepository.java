package at.fhooe.recyclingserver.jpa;

import at.fhooe.recyclingserver.model.Packaging;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface PackagingRepository extends JpaRepository<Packaging, Long> {

    Optional<Packaging> findPackagingByCode(String code);
}
