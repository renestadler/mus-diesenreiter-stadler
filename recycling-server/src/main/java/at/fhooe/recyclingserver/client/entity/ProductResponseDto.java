package at.fhooe.recyclingserver.client.entity;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ProductResponseDto {
    private String code;
    private long status;
    private ProductDto product;
}
